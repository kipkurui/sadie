from typing import Any

import pandas as pd

from sadie.airr.models import AirrSeriesModel


class AirrSeries(pd.Series):
    _metadata = ["meta"]  # add custom namespaces here

    def __init__(self, data: Any, copy: bool = False):
        super(AirrSeries, self).__init__(data=data, copy=copy)
        if not isinstance(data, pd.core.internals.managers.SingleBlockManager):
            if isinstance(data, pd.core.series.Series):
                self._verify()

    @property
    def _constructor(self) -> "AirrSeries":
        return AirrSeries  # type: ignore[return-value]

    def _verify(self) -> None:
        data = AirrSeriesModel(**self).dict()  # type: ignore
        self.update(data)