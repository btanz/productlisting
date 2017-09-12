
class PositionAuction:
    """Model position auctions for web platforms.

    Literature (excerpt):
    Varian, H. R. (2007): "Position auctions" International Journal of Industrial Organization
    Athey, S.; Ellision, G. (2011): "Position Auctions with consumer search" Quarterly Journal of Economics

    """

    def __init__(self, max_slots, valuations, ctrs):
        """Create instance of a position auction.

        Args:
            max_slots (int): The number of slots available in the auction.
            valuations (list of tuples (x, y), where (int) x is id and (int/float) y is valuation):
                List of bidder valuations.
                Example: [(1, 6.0), (2, 4.4), (3, 5.2)]
            ctrs (list of floats): Click-through-rates for all available slots, ordered from highest
                to lowest slot.

        """
        self.max_slots = max_slots
        self.valuations = valuations
        self.ctrs = ctrs

    @property
    def max_slots(self):
        """int: The number of slots available in the auction."""
        return self._max_slots

    @max_slots.setter
    def max_slots(self, m):
        if m <= 0:
            raise ValueError("Number of slots most be a positive integer")
        self._max_slots = m

    @property
    def ctrs(self):
        """list of floats: Click-through-rates for all available slots, ordered from highest to lowest slot."""
        return self._ctrs

    @ctrs.setter
    def ctrs(self, c):
        if sum(c) > 1:
            raise ValueError('Sum of CTRs cannot exceed 1')
        if not all(y== 0 or x > y for x, y in zip(c, c[1:])):
            raise ValueError('CTR-sequence must be strictly decreasing (or zero) over slots.')
        if self.max_slots > len(c):
            raise ValueError('A CTR must be available for all slots.')
        c[self.max_slots:] = [0] * (len(c) - self.max_slots)   # Enforce CTR=0 for all slots not shown/available
        self._ctrs = c

    @property
    def valuations(self):
        """list of tuples (x, y), where (int) x is id and (int/float) y is valuation: Bidder valuations."""
        return self._valuations

    @valuations.setter
    def valuations(self, v):
        if len(v) <= self.max_slots:
            raise ValueError('#Bidders must be larger than #slots.')
        self._valuations = v


    def __repr__(self):
        repr = "Position Auction \n" \
               "Total available slots: {0} \n" \
               "Bidder valuations: {1} \n" \
               "Click-through-rates: {2}"
        return repr.format(self.max_slots, self.valuations, self.ctrs)

    def compute_equilibrium(self):
        """Compute a symmetric Nash equilibrium of the generalized second price auction using
            the recursion developed in Varian (2007).

        Note:
            Generically and without further assumptions, there is no unique Nash equilibrium in pure strategies. However,
            the computed equilibrium is 'reasonable'.

        Returns:
            Dictionary containing
                'bids': A list of tuples (x, y) containing equilibrium bids x for all bidders y.
                'revenue': Expected revenue of the auction.

        """
        sorted_valuations = sorted(self.valuations, key=lambda x: x[1])
        ctrs = self.ctrs
        ctrs.extend([0] * (len(sorted_valuations)-len(ctrs)))
        ctrs = list(reversed(ctrs))
        num_bids = len(sorted_valuations)
        revenue = 0

        bids = []
        for i in range(num_bids):
            if i < (len(ctrs)-1) and ctrs[i+1] == 0:
                bid = 0
            elif i == 0:
                bid = (sorted_valuations[i][1] * (ctrs[i+1] - ctrs[i])) / ctrs[i+1]
                revenue += bid * ctrs[i+1]
            elif i == (num_bids-1):
                bid = (sorted_valuations[i][1] * (ctrs[i] - ctrs[i-1]) + bids[i - 2] * ctrs[i-1]) / ctrs[i]
                # note: No impact on revenue, since bid for highest slot is never paid
            else:
                bid = (sorted_valuations[i][1] * (ctrs[i+1] - ctrs[i]) + bids[i-1]*ctrs[i]) / ctrs[i+1]
                revenue += bid * ctrs[i + 1]
            bids.append(bid)

        return {'bids': sorted(list(zip([int(i[0]) for i in sorted_valuations], bids)), key=lambda x: x[0]), 'expected revenue': revenue}