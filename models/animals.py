from odoo import models, fields, api
from odoo.exceptions import UserError


class Animal(models.Model):
    _name = "animal"
    _description = "Animals table"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "identification desc"

    name = fields.Char(string="Nombre", required=True)
    sex = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino')
    ], string="Sexo", default="male")
    birthdate = fields.Date(string="Fecha de Nacimiento")
    # NUEVOS CAMPOS
    age = fields.Integer(string="Edad")
    reproductive_status = fields.Selection([
        ('neutered', 'Esterilizado'),
        ('entire', 'Entero'),
    ], string="Esterilizado/Entero")
    microchip_number = fields.Char(string="N° de microchip")

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

    # Antes: relación simple Many2many sin detalles.
    # Ahora: mantenemos 'vaccines' como campo calculado (solo lectura) para
    # mostrar el listado de vacunas únicas aplicadas, basado en 'vaccination_ids'.
    vaccines = fields.Many2many(
        "animal.vaccine",
        string="Vacunas",
        relation="animal_vaccine_rel",
        compute="_compute_vaccines",
        store=True,
        readonly=True,
    )
    # NUEVO: líneas de vacunación con detalles
    vaccination_ids = fields.One2many(
        "animal.vaccination",
        "animal_id",
        string="Vacunaciones"
    )

    # ===== NUEVO BLOQUE: Desparasitaciones =====
    dewormers = fields.Many2many(
        "animal.dewormer",
        string="Desparasitantes",
        relation="animal_dewormer_rel",
        compute="_compute_dewormers",
        store=True,
        readonly=True,
    )
    deworming_ids = fields.One2many(
        "animal.deworming",
        "animal_id",
        string="Desparasitaciones"
    )

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
    visit_count = fields.Integer(string="Visitas", compute="_compute_visit_count")

    # ===== NUEVOS CAMPOS SOLICITADOS (se guardan en BD) =====
    character = fields.Char(string="Carácter")
    habitat = fields.Char(string="Hábitat")
    treating_doctor = fields.Char(string="Médico tratante")
    hair_type = fields.Char(string="Tipo de pelo")
    diet = fields.Char(string="Dieta")

    @api.model
    def create(self, vals):
        if vals.get('identification', 'Nuevo') == 'Nuevo':
            vals['identification'] = self.env['ir.sequence'].next_by_code('animal.identification') or 'Nuevo'
        return super(Animal, self).create(vals)

    @api.depends('vaccination_ids.vaccine_id')
    def _compute_vaccines(self):
        for record in self:
            vaccine_ids = record.vaccination_ids.mapped('vaccine_id').ids if record.vaccination_ids else []
            record.vaccines = [(6, 0, vaccine_ids)]

    @api.depends('deworming_ids.dewormer_id')
    def _compute_dewormers(self):
        for record in self:
            dewormer_ids = record.deworming_ids.mapped('dewormer_id').ids if record.deworming_ids else []
            record.dewormers = [(6, 0, dewormer_ids)]

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
            'name': 'Presupuestos',
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
            'name': 'Facturas',
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
            'name': 'Visitas',
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
            'name': 'Nuevo Presupuesto',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': self.owner.id,  # Prellenar el cliente con el dueño del animal
            },
        }