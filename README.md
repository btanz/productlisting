# Auction-based product listings (prototype)
The purpose of this app-prototype is to illustrate equilibrium-bidding for slots and positions on a product plattform given valuations for these slots and positions. The app is written in Python using Django. More details below.

### Setup
* There are 15 products from 3 brands/labels
* Only 6 Slots with products can be displayed to a visitor for a given visit. 
* For displayed slots, there is a strictly positive click-through-rate (CTR) that is strictly decreasing with positions (the further down the page, the lower the CTR). CTRs could be calibrated from actual data, but are assumed for the purpose of this app.
* The CTR is zero for slots/products not displayed.
* Brands/labels/sellers receive some benefit if a product is clicked (Suppose, with some loss of generality, a click is a purchase of a single product item.) The valuation quantifies this benefit.
* Valuations vary across products and can be interpreted as the unit margin of a product (before paying for clicks). Generally, the higher the unit margin, the higher the valuation of a slot. 
* Products compete for available slots and the position of the slot on the page

### Process
Visiting the page or clicking on "Refresh" causes the following actions:
* Valuations are drawn from a distribution (valuations are assumed i.i.d Normal) 
* Equilbrium bids are computed - In particular, a set of equilibrium bids for a symmetric Nash-equilibrium of a generalized second-price-auction is computed. Note: Generically, there are multiple equilibria.
* Expected revenue (to the plattform) is computed
* Products are displayed in the order of bids
* Other statistics - such as equilibrium bids and the auction revenue - are displayed. 

### Assumptions and discussion (excerpt)
* CTRs only depend on slot position (and hence not on the product shown at a position). Comment: Validity of this assumption depends on the category. Assumption can be relaxed by introducing another parameter.
* Payments occur per (hypothetical) click on a product. Comment: This is a simplification, since there may be more steps necessary for a conversion (or valuations already account for it).
* Valuations for a given product are uncorrelated over time/requests. In practice, valuations are probably correlated. For example, if a certain product is in stock, the valuation is likely rather constant over time. If the product is no longer in stock, however, the valuation may drop to zero.
* Note: All assumption can be relaxed.

### Notes
* Bidder in position x pays bid of bidder x-1 per click (second-price-auction)
* Expected revenue accounts for the possibility of no click (and hence no revenue) in case the sum of CTRs is less than one


### References
Varian, H. R. (2007): "Position auctions" International Journal of Industrial Organization

Athey, S.; Ellision, G. (2011): "Position Auctions with consumer search" Quarterly Journal of Economics
