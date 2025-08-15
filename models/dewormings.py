from odoo import models, fields, api


class Dewormer(models.Model):
    _name = "animal.dewormer"
    _description = "Catálogo de desparasitantes (antiparasitarios)"

    name = fields.Char(string="Desparasitante", required=True)
    description = fields.Text(string="Descripción")


class Deworming(models.Model):
    _name = "animal.deworming"
    _description = "Registro de desparasitación por animal"
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
    dewormer_id = fields.Many2one(
        "animal.dewormer",
        string="Desparasitante",
        required=True,
        ondelete="restrict",
        tracking=True,
    )

    # Datos de la aplicación
    date = fields.Date(string="Fecha de desparasitación", required=True, tracking=True)
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
    next_date = fields.Date(string="Próxima desparasitación", tracking=True)
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
            label = "%s" % (rec.dewormer_id.name if rec.dewormer_id else "Desparasitación")
            if rec.date:
                label += " - %s" % fields.Date.to_string(rec.date)
            res.append((rec.id, label))
        return res

    _sql_constraints = [
        # Evitar duplicados exactos (mismo animal, mismo desparasitante, misma fecha)
        ('unique_animal_dewormer_date',
         'unique(animal_id, dewormer_id, date)',
         'Ya existe un registro de esta desparasitación para el animal en la misma fecha.')
    ]
