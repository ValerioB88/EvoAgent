# Index
<ul>
  {% for post in site.posts %}
    <li>
      <a href="/EvoAgent/{{ post.url }}">{{ post.title }} {{ post.date }}</a>
    </li>
  {% endfor %}
</ul>
