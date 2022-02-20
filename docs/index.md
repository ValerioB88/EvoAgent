# Index
<ul>
  {% for post in site.posts %}
    <li>
      <a href="/EvoAgent/{{ post.url }}"><span style="color:blue">{{ page.date | date_to_long_string: "ordinal", "US" }}</span> {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
