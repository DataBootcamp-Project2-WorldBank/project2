html_layout = """
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS  -- Commented out to use Bootswatch
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
    -->
     <!-- Bootwatch core CSS -->
    <link rel="stylesheet" href="/static/css/bootstrap.css">

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.3/dist/leaflet.css"
    integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
    crossorigin=""/>

    <!-- d3 JavaScript -->
    <script src="https://d3js.org/d3.v5.min.js"></script>

    <!-- SimpleTables -->
    <link href="https://cdn.jsdelivr.net/npm/simple-datatables@latest/dist/style.css" rel="stylesheet" type="text/css">
    <script src="https://cdn.jsdelivr.net/npm/simple-datatables@latest" type="text/javascript"></script>
    
    <!-- Our Maps CSS -->
    <link rel="stylesheet" type="text/css" href="static/css/maps.css">
    <!-- General Style -->
    <link rel="stylesheet" type="text/css" href="static/css/style.css">

    {% if title %}
    <title>{{ title }} - Project 2</title>
    {% else %}
    <title>Welcome to Project 2</title>
    {% endif %}

  </head>

  <body>
         <!-- navbar -->
         <div class="navbar navbar-expand-lg fixed-top navbar-dark bg-primary">
            <div class="container">
              <a href="{{ url_for('index') }}" class="navbar-brand">World Bank Projects Performance Analysis</a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarResponsive">

                {% if not current_user.is_anonymous %}
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0 ">
                  <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
                        data-bs-toggle="dropdown" aria-expanded="false">
                        Data
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li><a class="dropdown-item" href="{{ url_for('iegdataview') }}">IEG</a></li>
                        <li><a class="dropdown-item" href="{{ url_for('gdpdataview') }}">GDP</a></li>
                        <li><a class="dropdown-item" href="{{ url_for('cpidataview') }}">CPI</a></li>
                        <li><a class="dropdown-item" href="{{ url_for('popdataview') }}">Population</a></li>
                    </ul>
                  </li>
                </ul>
                {% endif %}
                <ul class="navbar-nav ms-auto ml-auto mb-2 mb-lg-0 ">
                  <li class="nav-item">
                  {% if current_user.is_anonymous %}
                  <a class="nav-link" href="{{ url_for('login') }}">Login</a>
                  {% else %}
                  <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                  {% endif %}
                  </li>
                </ul>
              </div>
            </div>
          </div>

      <!-- main page -->
      <div class="container">
        <div class="row">

        <div class="col-md-3">
          <!-- Menu Links -->
          {% if not current_user.is_anonymous %}
            <ul class="list-group">
              <a href="#" class="list-group-item list-group-item-action active"></a>
              <a href="{{url_for('index')}}" class="list-group-item list-group-item-action">Home</a>
              <a href="{{ url_for('aboutproject') }}" class="list-group-item list-group-item-action">About Project</a>
              <a href="/dashapp/" class="list-group-item list-group-item-action">Projects Chart</a>
            </ul>
            <ul class="list-group">
              <a href="#" class="list-group-item list-group-item-action active">Analysis</a>
              <a href="{{url_for('gdpanalysis')}}" class="list-group-item list-group-item-action">Gross Domestic Product</a>
              <a href="{{url_for('poplevel')}}" class="list-group-item list-group-item-action">Population Levels</a>
              <a href="#" class="list-group-item list-group-item-action">Corruption Index</a>
            </ul>
            <ul class="list-group mt-5">
              <a href="#" class="list-group-item list-group-item-action active">Data Sets</a>
              <a href="{{ url_for('iegdataview') }}" class="list-group-item list-group-item-action">Project Performance</a>
              <a href="{{ url_for('gdpdataview') }}" class="list-group-item list-group-item-action">Gross Domestic Product</a>
              <a href="{{ url_for('cpidataview') }}" class="list-group-item list-group-item-action">Corruption Prevention Idx</a>
              <a href="{{ url_for('popdataview') }}" class="list-group-item list-group-item-action">Population Levels</a>
            </ul>
          </div>
          {% endif %}

          <div class="col-md-9">
            <!-- Messages -->
            {% with messages = get_flashed_messages() %}
            {% if messages %}
            <ul>
                {% for message in messages %}
                <li>{{ message }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            {% endwith %}

            <!-- Main block feature -->
            {% block content %}{% endblock %}
          </div>

          </div>
      </div>

    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.3.3/dist/leaflet.js"
    integrity="sha512-tAGcCfR4Sc5ZP5ZoVz0quoZDYX5aCtEm/eu1KhSLj2c9eFrylXZknQYmxUssFaVJKvvc0dJQixhGjG2yXWiV9Q=="
    crossorigin=""></script>
    <script type="text/javascript" src="static/js/leaflet.pattern.js"></script>
    <!-- API key -->
    <script type="text/javascript" src="static/js/config.js"></script>
    <!-- JS  -->
    <script type="text/javascript" src="static/js/plotmap.js"></script>
    <script type="text/javascript" src="static/js/poplevel.js"></script>
    <!-- D3.js -->
    <script src="https://d3js.org/d3.v5.min.js"></script>
		<script src="https://cdnjs.cloudflare.com/ajax/libs/d3-tip/0.7.1/d3-tip.min.js"></script>
  </body>
</html>
"""