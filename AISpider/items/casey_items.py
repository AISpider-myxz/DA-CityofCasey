from . import BaseItem
from scrapy import Field


class CaseyItem(BaseItem):
    app_number = Field()
    estate_name = Field()
    description = Field()
    lodged = Field()
    estimated_value = Field()
    status = Field()
    further_info_requested_date = Field()
    further_info_received_date = Field()
    advertising_commencement = Field()
    advertising_completion = Field()
    no_of_objections = Field()
    responsible_authority_outcome = Field()
    final_outcome = Field()
    final_outcome_date = Field()
    vcat_lodged_date = Field()
    system_status = Field()
    versio_lodged_date = Field()
    permit_ext_start_date = Field()
    permit_ext_end_date = Field()
    property_address = Field()
    land_description = Field()


    class Meta:
        table = 'casey'
        unique_fields = ['app_number', ]
