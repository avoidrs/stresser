from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    attackState = State()

    lookupState = State()


class AdminStates(StatesGroup):
    addMassDaysState = State()
    addPlanState = State()
    searchUserState = State()
    bcState = State()
    removePlanState = State()