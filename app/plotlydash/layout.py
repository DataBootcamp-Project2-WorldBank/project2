html_layout = """
<{% extends "base.html" %}


{% block content %}
  <section>
    
  </section>
    {% for post in posts %}
  <!--  <div><p>{{ post.author.username }} says: <b>{{ post.body }}</b></p></div> -->
    {% endfor %}
    {%app_entry%}
      <footer>
          {%config%}
          {%scripts%}
          {%renderer%}
        </footer>
{% endblock %}

    
"""