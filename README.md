# StockBoy

Librairies pip : pip install -r /path/to/requirements.txt

Autre librairie requise:
sudo apt-get install libatlas-base-dev

Pour le fichier de config json des webhooks (qui se trouve dans le répertoire en amont): 

{
  
        "url": "https://discord.com/api/webhooks/...",
        "url2": "https://discord.com/api/webhooks/...",
        "url3": "https://discord.com/api/webhooks/..."
        ...
        "urln": ...

}

Ne pas oublier également le fichier .env qui contient le token du bot discord qui roule. Il doit se trouver dans le même répertoire que bot.py
