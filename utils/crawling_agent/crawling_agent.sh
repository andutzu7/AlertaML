#!/bin/sh

while IFS= read -r link; do
  wget -q --spider -r -p -nd $link
done < utils/crawling_agent/web_pages