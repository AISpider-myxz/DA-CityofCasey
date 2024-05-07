from sqlalchemy import Column, String, Text, Integer, DateTime, func
from .moretonbay import Base


class Penrith(Base):
    __tablename__ = 'casey'

    id = Column(Integer, primary_key=True, autoincrement=True)

    app_number = Column(String(255), nullable=False, unique=True)
    estate_name = Column(String(255), nullable=True, server_default=None)
    description = Column(Text, nullable=True, server_default=None)
    lodged = Column(Integer, nullable=True)
    estimated_value = Column(String(2555), nullable=False,server_default=None)
    status = Column(String(255), nullable=True, server_default=None)
    further_info_requested_date = Column(Integer, nullable=True)
    further_info_received_date = Column(Integer, nullable=True)
    advertising_commencement = Column(String(255), nullable=True, server_default=None)
    advertising_completion = Column(String(255), nullable=True, server_default=None)
    no_of_objections = Column(String(255), nullable=True, server_default=None)
    responsible_authority_outcome = Column(String(255), nullable=True, server_default=None)
    final_outcome = Column(String(255), nullable=True, server_default=None)
    final_outcome_date = Column(Integer, nullable=True,)
    vcat_lodged_date = Column(Integer, nullable=True,)
    system_status = Column(String(255), nullable=True, server_default=None)
    versio_lodged_date = Column(Integer, nullable=True,)
    permit_ext_start_date = Column(Integer, nullable=True,)
    permit_ext_end_date = Column(Integer, nullable=True,)
    property_address = Column(Text, nullable=True, server_default=None)
    land_description = Column(Text, nullable=True, server_default=None)

    _tid = Column(String(255), nullable=False,server_default=None)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
