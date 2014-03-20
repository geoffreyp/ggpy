from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
from .geom import geom


class geom_tile(geom):
    VALID_AES = ['x', 'y', 'fill']

    def plot_layer(self, data, ax):
        groups = {'fill'}
        groups = groups & set(data.columns)
        if groups:
            for name, _data in data.groupby(list(groups)):
                _data = _data.to_dict('list')
                for ae in groups:
                    _data[ae] = _data[ae][0]
                self._plot(_data, ax)
        else:
            _data = data.to_dict('list')
            self._plot(_data, ax)

    def plot_layer(self, layer, ax):
        layer = dict((k, v) for k, v in layer.iteritems() if k in self.VALID_AES)
        layer.update(self.manual_aes)

        x = layer.pop('x')
        y = layer.pop('y')
        fill = layer.pop('fill')
        X = pd.DataFrame({'x': x,
                          'y': y,
                          'fill': fill}).set_index(['x', 'y']).unstack(0)
        x_ticks = range(0, len(set(x)))
        y_ticks = range(0, len(set(y)))

        ax.imshow(X, interpolation='nearest', **layer)
        ax.set_xticklabels(x)
        ax.set_xticks(x_ticks)
        ax.set_yticklabels(y)
        ax.set_yticks(y_ticks)
