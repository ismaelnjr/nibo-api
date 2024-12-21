from uuid import UUID
from typing import Optional, List, Any
from datetime import datetime


class CategoryElement:
    id: UUID
    category_id: UUID
    category_name: str
    value: float
    description: str
    type: str
    parent: str
    parent_id: UUID

    def __init__(self, id: UUID, category_id: UUID, category_name: str, value: float, description: str, type: str, parent: str, parent_id: UUID) -> None:
        self.id = id
        self.category_id = category_id
        self.category_name = category_name
        self.value = value
        self.description = description
        self.type = type
        self.parent = parent
        self.parent_id = parent_id


class StakeholderClass:
    id: UUID
    name: str
    is_deleted: bool
    type: str
    cpf_cnpj: Optional[str]

    def __init__(self, id: UUID, name: str, is_deleted: bool, type: str, cpf_cnpj: Optional[str]) -> None:
        self.id = id
        self.name = name
        self.is_deleted = is_deleted
        self.type = type
        self.cpf_cnpj = cpf_cnpj


class CustomAttributes:
    pass

    def __init__(self, ) -> None:
        pass


class Recurrence:
    id: UUID
    interval: int
    interval_type: int
    interval_type_description: str
    end_type: int
    end_type_description: str
    provision_in_advance: int
    base_day: int

    def __init__(self, id: UUID, interval: int, interval_type: int, interval_type_description: str, end_type: int, end_type_description: str, provision_in_advance: int, base_day: int) -> None:
        self.id = id
        self.interval = interval
        self.interval_type = interval_type
        self.interval_type_description = interval_type_description
        self.end_type = end_type
        self.end_type_description = end_type_description
        self.provision_in_advance = provision_in_advance
        self.base_day = base_day


class RecebivelItem:
    categories: List[CategoryElement]
    cost_centers: List[Any]
    schedule_id: UUID
    type: str
    is_entry: bool
    is_bill: bool
    is_debit_note: bool
    is_flagged: bool
    is_dued: bool
    due_date: datetime
    accrual_date: datetime
    schedule_date: datetime
    create_date: datetime
    create_user: str
    update_date: datetime
    update_user: str
    value: float
    is_paid: bool
    cost_center_value_type: int
    paid_value: float
    open_value: float
    stakeholder_id: UUID
    stakeholder: StakeholderClass
    description: str
    reference: str
    category: StakeholderClass
    has_installment: bool
    has_recurrence: bool
    recurrence: Recurrence
    has_open_entry_promise: bool
    has_entry_promise: bool
    auto_generate_entry_promise: bool
    has_invoice: bool
    has_pending_invoice: bool
    has_schedule_invoice: bool
    custom_attributes: CustomAttributes
    auto_generate_nf_se_type: int
    is_payment_scheduled: bool

    def __init__(self, categories: List[CategoryElement], cost_centers: List[Any], schedule_id: UUID, type: str, is_entry: bool, is_bill: bool, is_debit_note: bool, is_flagged: bool, is_dued: bool, due_date: datetime, accrual_date: datetime, schedule_date: datetime, create_date: datetime, create_user: str, update_date: datetime, update_user: str, value: float, is_paid: bool, cost_center_value_type: int, paid_value: float, open_value: float, stakeholder_id: UUID, stakeholder: StakeholderClass, description: str, reference: str, category: StakeholderClass, has_installment: bool, has_recurrence: bool, recurrence: Recurrence, has_open_entry_promise: bool, has_entry_promise: bool, auto_generate_entry_promise: bool, has_invoice: bool, has_pending_invoice: bool, has_schedule_invoice: bool, custom_attributes: CustomAttributes, auto_generate_nf_se_type: int, is_payment_scheduled: bool) -> None:
        self.categories = categories
        self.cost_centers = cost_centers
        self.schedule_id = schedule_id
        self.type = type
        self.is_entry = is_entry
        self.is_bill = is_bill
        self.is_debit_note = is_debit_note
        self.is_flagged = is_flagged
        self.is_dued = is_dued
        self.due_date = due_date
        self.accrual_date = accrual_date
        self.schedule_date = schedule_date
        self.create_date = create_date
        self.create_user = create_user
        self.update_date = update_date
        self.update_user = update_user
        self.value = value
        self.is_paid = is_paid
        self.cost_center_value_type = cost_center_value_type
        self.paid_value = paid_value
        self.open_value = open_value
        self.stakeholder_id = stakeholder_id
        self.stakeholder = stakeholder
        self.description = description
        self.reference = reference
        self.category = category
        self.has_installment = has_installment
        self.has_recurrence = has_recurrence
        self.recurrence = recurrence
        self.has_open_entry_promise = has_open_entry_promise
        self.has_entry_promise = has_entry_promise
        self.auto_generate_entry_promise = auto_generate_entry_promise
        self.has_invoice = has_invoice
        self.has_pending_invoice = has_pending_invoice
        self.has_schedule_invoice = has_schedule_invoice
        self.custom_attributes = custom_attributes
        self.auto_generate_nf_se_type = auto_generate_nf_se_type
        self.is_payment_scheduled = is_payment_scheduled


class RecebivelList:
    items: List[RecebivelItem]
    count: int

    def __init__(self, items: List[RecebivelItem], count: int) -> None:
        self.items = items
        self.count = count