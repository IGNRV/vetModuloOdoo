from odoo import models, fields, api
from odoo.exceptions import UserError


class Animal(models.Model):
    _name = "animal"
    _description = "Animals table"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order ="identification desc"

    name = fields.Char(string="Nombre", required=True)
    sex = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino')
    ], string="Sexo", default="male")
    birthdate = fields.Date(string="Fecha de Nacimiento")
    photo = fields.Binary(string="Foto")
    breed = fields.Many2one("animal.breed", string="Raza")
    species = fields.Many2one("animal.specie", string="Especie", required=True)
    owner = fields.Many2one('res.partner', string="Dueño", store=True)
    weight = fields.Float(string="Peso")
    height = fields.Float(string="Altura")
    size = fields.Selection([
        ('small', 'Pequeño'),
        ('medium', 'Mediano'),
        ('large', 'Grande'),
    ], string="Tamaño", default='small')
    medicines = fields.Many2many("animal.medicine", string="Medicamentos", relation="animal_medicine_rel")
    vaccines = fields.Many2many("animal.vaccine", string="Vacunas", relation="animal_vaccine_rel")
    diseases = fields.Many2many("animal.disease", string="Enfermedades", relation="animal_disease_rel")
    allergies = fields.Many2many("animal.allergy", string="Alergias", relation="animal_allergy_rel")
    surgeries = fields.Many2many("animal.surgery", string="Cirugías", relation="animal_surgery_rel")
    visit_ids = fields.One2many('animal.visit', 'animal_id', string='Visitas')
    active = fields.Boolean(string="Activo", default=True)
    tags = fields.Many2many("animal.tag", string="Etiquetas", relation="animal_tag_rel")
    insurance = fields.Many2one("animal.insurance", string="Seguro", relation="animal_insurance_rel")
    identification = fields.Char(string="ID", required=True, copy=False, readonly=True, index=True, default=lambda self: 'Nuevo')
    internal_notes = fields.Text(string="Notas")
    quote_count = fields.Integer(string="Presupuestos", compute="_compute_quote_count")
    invoice_count = fields.Integer(string="Facturas", compute="_compute_invoice_count")
    visit_count = fields.Integer(string="Visits", compute="_compute_visit_count")



    @api.model
    def create(self, vals):
        if vals.get('identification', 'Nuevo') == 'Nuevo':
            vals['identification'] = self.env['ir.sequence'].next_by_code('animal.identification') or 'Nuevo'
        return super(Animal, self).create(vals)

    @api.depends('owner')
    def _compute_quote_count(self):
        for record in self:
            if record.owner:
                record.quote_count = self.env['sale.order'].search_count([('partner_id', '=', record.owner.id)])
            else:
                record.quote_count = 0

    @api.depends('owner')
    def _compute_invoice_count(self):
        for record in self:
            if record.owner:
                record.invoice_count = self.env['account.move'].search_count([('partner_id', '=', record.owner.id)])
            else:
                record.invoice_count = 0

    @api.depends('owner')
    def _compute_visit_count(self):
        for record in self:
            if record.id:
                record.visit_count = self.env['animal.visit'].search_count([('animal_id', '=', record.id)])
            else:
                record.visit_count = 0

    def action_view_quotes(self):
        # Obtener el ID del partner asociado
        partner_id = self.owner.id

        return {
            'name': 'Quotes',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('partner_id', '=', partner_id)],
            'context': dict(self._context),
        }

    def action_view_invoices(self):
        # Obtener el ID del partner asociado
        partner_id = self.owner.id

        return {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('partner_id', '=', partner_id)],
            'context': dict(self._context),
        }

    def action_view_visits(self):
        # Obtener el ID del partner asociado
        animal = self.id

        return {
            'name': 'Visits',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'animal.visit',
            'domain': [('animal_id', '=', animal)],
            'context': dict(self._context),
        }

    def action_create_quote(self):
        # Asegurarse de que el animal tiene un dueño
        if not self.owner:
            raise UserError('This animal does not have an owner defined.')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Nuevo Quote',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': self.owner.id,  # Prellenar el cliente con el dueño del animal
            },
        }