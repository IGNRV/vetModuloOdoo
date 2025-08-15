from odoo import models, fields, api

class Vaccine(models.Model):
    _name = "animal.vaccine"
    _description = "Animal vaccines table"

    name = fields.Char(string="Vacuna", required=True)
    description = fields.Text(string="Descripción")


class Vaccination(models.Model):
    _name = "animal.vaccination"
    _description = "Registro de vacunación por animal"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date desc, id desc"

    # Enlaces
    animal_id = fields.Many2one(
        "animal",
        string="Animal",
        required=True,
        ondelete="cascade",
        index=True,
        tracking=True,
    )
    vaccine_id = fields.Many2one(
        "animal.vaccine",
        string="Vacuna",
        required=True,
        ondelete="restrict",
        tracking=True,
    )

    # Datos de la aplicación
    date = fields.Date(string="Fecha de vacunación", required=True, tracking=True)
    route = fields.Selection([
        ('sc', 'Subcutánea'),
        ('im', 'Intramuscular'),
        ('iv', 'Intravenosa'),
        ('oral', 'Oral'),
        ('intranasal', 'Intranasal'),
        ('topical', 'Tópica'),
        ('other', 'Otra'),
    ], string="Vía de administración", tracking=True)
    doctor = fields.Char(string="Dr/Dra (aplicó)", tracking=True)
    next_date = fields.Date(string="Próxima vacunación", tracking=True)
    notes = fields.Text(string="Notas/Observaciones")

    # Auxiliares de lectura
    owner_id = fields.Many2one(
        related="animal_id.owner",
        string="Dueño",
        store=True,
        readonly=True
    )
    specie_id = fields.Many2one(
        related="animal_id.species",
        string="Especie",
        store=True,
        readonly=True
    )

    @api.onchange('animal_id')
    def _onchange_animal_id_prefill_doctor(self):
        """Si el animal tiene 'médico tratante', proponerlo como doctor."""
        for rec in self:
            if rec.animal_id and rec.animal_id.treating_doctor and not rec.doctor:
                rec.doctor = rec.animal_id.treating_doctor

    def name_get(self):
        res = []
        for rec in self:
            label = "%s" % (rec.vaccine_id.name if rec.vaccine_id else "Vacuna")
            if rec.date:
                label += " - %s" % fields.Date.to_string(rec.date)
            res.append((rec.id, label))
        return res

    _sql_constraints = [
        # Evitar duplicados exactos (mismo animal, misma vacuna, misma fecha)
        ('unique_animal_vaccine_date',
         'unique(animal_id, vaccine_id, date)',
         'Ya existe un registro de esta vacuna para el animal en la misma fecha.')
    ]
