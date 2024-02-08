# Copyright 2024 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from zipline.pipeline import master, EquityPricing

def CommonStocks():
    """
    Return a Pipeline filter that is limited to domestic common stocks, excluding
    secondary shares. This filter is intended to be used as the initial_universe
    of the Pipeline.
    """
    category = master.SecuritiesMaster.sharadar_Category.latest
    common_stocks = (
        # domestic common stocks
        category.has_substring("Domestic Common")
        # no secondary shares
        & ~category.has_substring("Secondary")
    )
    return common_stocks

def BaseUniverse():
    """
    Return a Pipeline filter that excludes illiquid stocks and penny stocks.
    This filter is intended to be used as the screen of the Pipeline or the
    mask of factors in the Pipeline.
    """
    base_universe = (EquityPricing.volume.latest > 0).all(21)
    base_universe = (EquityPricing.close.latest > 1.00).all(21, mask=base_universe)

    return base_universe
