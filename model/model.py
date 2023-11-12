import datetime as dt


class Monte_Carlo_Simulator:

    def __init__(self,
                 no_simulations: int,
                 no_days: int,
                 cVaR_alpha: float,
                 VaR_alpha: float):

        self.no_simulations = no_simulations
        self.no_days = no_days
        self.cVaR_alpha = cVaR_alpha
        self.VaR_alpha = VaR_alpha
        self.start_time = None
        self.end_time = None

    def

