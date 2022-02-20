# Index
<ul>
  {% for post in site.posts %}
    <li>
      <a href="/EvoAgent/{{ post.url }}"><style="color:blue">{{ page.date| date: "%m-%d-%Y" }}</style> {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
