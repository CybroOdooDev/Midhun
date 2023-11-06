from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    activate_rss_feed = fields.Boolean(
        string="Activate RSS Feed",
        config_parameter='txs_soar.activate_rss_feed')
    rss_feed_url = fields.Char(string="Rss Feed Url",
                               help="Enter the RSS Feed Url",
                               config_parameter='txs_soar.rss_feed_url')
