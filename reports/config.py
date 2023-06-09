
from pathlib import Path

BASE_PATH = Path.cwd() / 'data'

LOGO = 'data:image/jpeg;base64,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'

DICT_Y = {
            'PRCP':('value_mean','Média da Precipitação')
            , 'TAVG':('value_mean','Média da Temperatura')
            , 'TMAX':('value_max','Máxima da Temperatura')
            , 'TMIN':('value_min','Mínima da Temperatura')
        }

DICT_TIPO_VINHO = {
    'Pinot Noir': 'tinto',
    'Cabernet Sauvignon': 'tinto',
    'Red Blend': 'tinto',
    'Bordeaux-style Red Blend': 'tinto',
    'Merlot': 'tinto',
    'Syrah': 'tinto',
    'Nebbiolo': 'tinto',
    'Zinfandel': 'tinto',
    'Sangiovese': 'tinto',
    'Malbec': 'tinto',
    'Portuguese Red': 'tinto',
    'Tempranillo': 'tinto',
    'Rhône-style Red Blend': 'tinto',
    'Cabernet Franc': 'tinto',
    'Gamay': 'tinto',
    'Shiraz': 'tinto',
    'Petite Sirah': 'tinto',
    'Sangiovese Grosso': 'tinto',
    'Barbera': 'tinto',
    'Tempranillo Blend': 'tinto',
    'Carmenère': 'tinto',
    'Port': 'tinto',
    'Grenache': 'tinto',
    'Corvina, Rondinella, Molinara': 'tinto',
    'Tannat':'tinto',
    'Cabernet Sauvignon-Merlot':'tinto',
    'Merlot-Cabernet Sauvignon':'tinto',
    #------------------------------------
    'Chardonnay': 'branco',
    'Riesling': 'branco',
    'Sauvignon Blanc': 'branco',
    'White Blend': 'branco',
    'Pinot Gris': 'branco',
    'Grüner Veltliner': 'branco',
    'Portuguese White': 'branco',
    'Bordeaux-style White Blend': 'branco',
    'Pinot Grigio': 'branco',
    'Gewürztraminer': 'branco',
    'Viognier': 'branco',
    'Glera': 'branco',
    'Chenin Blanc': 'branco',
    #------------------------------------
    'Sparkling Blend': 'espumante',
    'Portuguese Sparkling':'espumante',
    'Champagne Blend': 'espumante',
    'Moscatel':'espumante',
}