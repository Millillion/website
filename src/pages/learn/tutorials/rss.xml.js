import { streamRss } from "../../../lib/learn-rss.js";

export const GET = (context) => streamRss(context, "tutorials");
