# Index
<ul>
  {% for post in site.posts %}
    <li>
      <a href="/EvoAgent/{{ post.url }}">aa{{ post.date | date_to_long_string: "ordinal", "US" }}{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
