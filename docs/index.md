# Index
<style>
  a { color: cyan;
outline: none;
text-decoration: none}
a:hover { border-bottom: 1px solid;
background: green}
   .tab {
            display: inline-block;
            margin-left: 40px;
    </style>

<ul>
  {% for post in site.posts %}
    <li>
      <a href="/EvoAgent/{{ post.url }}"><span style="color:magenta">{{ post.date | date: "%m/%d/%Y" }}<span class="tab"></span>{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
