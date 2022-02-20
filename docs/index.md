# Index
<ul>
  {% for post in site.posts %}
    <li>
      <a href="/EvoAgent/{{ post.url }}"><span style="color:blue">{{ page.date | date: "%m-%d-%Y" }}</span> {{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
