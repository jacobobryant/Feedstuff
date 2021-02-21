# Feedstuff

Some code for sharing stuff you like via Atom feeds.

Conceptually, this is nothing new. However, I hope the implementation I've come up with is helpful for others.
The more convenient it is to use protocols, the more people will actually use them.

## Interface

You publish a (paginated) Atom feed that describes your interactions with content/stuff/anything that has a URL. For example:
```xml
<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>https://feed.jacobobryant.com</id>
  <title>Jacob O'Bryant</title>
  <updated>2021-02-20T23:37:53.351669+00:00</updated>
  <link href="https://feed.jacobobryant.com" rel="self"/>
  <link href="https://jacobobryant.com" rel="alternate"/>
  <entry>
    <id>https://www.youtube.com/watch?v=dQw4w9WgXcQ</id>
    <title>Rick Astley - Never Gonna Give You Up</title>
    <updated>2021-02-20T23:37:53.404312+00:00</updated>
    <link href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" rel="alternate"/>
    <summary>Never gets old</summary>
    <category term="4-stars"/>
    <published>2021-02-20T20:57:15+00:00</published>
  </entry>
  ...
</feed>
```

You follow other people by subscribing to their feeds. If you don't already use a feed reader, you can subscribe via email with [Blogtrottr](https://blogtrottr.com/).
You should subscribe to my feed: `https://feed.jacobobryant.com`.

## Implementation

I use a bookmarklet for importing data, Airtable to store the data, and Repl.it to convert it into a feed. You can too with just a few steps:

1. Create an Airtable table with the following columns and types: `URL` (URL), `Title` (single line text),
   `Description` (long text), `Image` (URL), `Tags` (single line text), `Commentary` (long text), `Rating` (star rating).
   For convenience, you can [view my template](https://airtable.com/universe/expgM3ccityFHnIQZ/feedstuff-template) and click `Copy base`.
   
2. Add a Form view to your table, then click `Open form`. Copy the URL, and set `airtable_form_url` in the code below to it.
In your desktop web browser, create a bookmark, and paste in this code instead of a URL.

```javascript
javascript:(function () {
  let airtable_form_url = "https://airtable.com/shrabc123";
  let q = (s) => document.querySelector(s);
  let get = (m, k) => m ? m[k] : null;
  let title = get(q('title'), 'innerHTML') || "";
  let description = get(q('meta[name=description]'), 'content') ||
      get(q("meta[property='og:description']"), 'content') ||
      get(q("meta[property='twitter:description']"), 'content') || "";
  let image = get(q('meta[name=image]'), 'content') ||
      get(q("meta[property='og:image']"), 'content') ||
      get(q("meta[property='twitter:image']"), 'content') || "";
  var feed = get(q("link[type='application/atom+xml']"), 'href') ||
      get(q("link[type='application/rss+xml']"), 'href') || "";
  window.location = airtable_form_url +
      "?prefill_URL=" + encodeURIComponent(document.location) +
      "&prefill_Title=" + encodeURIComponent(title) +
      "&prefill_Description=" + encodeURIComponent(description) +
      "&prefill_Image=" + encodeURIComponent(image);
})()
```

3. Whenever you're on a web page that you want to share, click the bookmarklet you just created. It will extract metadata from the current
    page and use it to prefill the Airtable form.
    
4. Go to https://repl.it/github/jacobobryant/feedstuff, which will deploy this repo on your own Replit account. Copy the `.env.TEMPLATE`
   file to `.env` and paste in your Base ID (get it [from here](https://airtable.com/api)) and your API key (get it [from here](https://airtable.com/account)).
   (You should update the other config values too).
   
5. Click `Run`. The app will sync the contents of your Airtable table and serve it as an Atom feed. For example: `curl https://Feedstuff.jobryant.repl.co`.

6. Comment on [this issue](https://github.com/jacobobryant/Feedstuff/issues/1) and include the URL for your feed, so we can, you know, follow each other and stuff.

You can use a custom domain for your Replit app, and if you pay, you can prevent it from sleeping.

## Vision

I don't (necessarily) think we need completely distributed social networks, but it would be a step forward if everyone had
their own feed like the one I've described here. Ideally, we'd have a much beefier version of this Replit app. It would
have a plugin system so you could connect to other services besides just Airtable. e.g. import your tweets, your Spotify listening history, etc., then
it'll publish it all into a single feed. All your data in one place. Then other (potentially commercial) apps could build on top of that feed.

For example, if your feed includes entries for people you follow, it would be easy to write a crawler and index a bunch of these feeds
into a single database. From there you could provide search and recommendation APIs/UIs. At scale, this would be great.
The big commercial platforms would have more competition, and if we're lucky, information discovery would improve.

(Also, you could mark certain entries as private, so apps would need to get authorization--perhaps via oauth--to see them.)

The hard question is how do you get a bunch of people to actually start using an open protocol. The simpler
and easier it is, the better. Also, there needs to be an immediate benefit to using the protocol, not just "it'll be worth it in 10 years."

I got this idea for wiring up Airtable and Repl.it this morning and hacked it up in a few hours. It's really just an experiment. At a minimum,
I'll be using Airtable to curate content for a newsletter I'm planning to start soon. If I can think of additional immediate uses, then great (let
me know if you have any).
   
