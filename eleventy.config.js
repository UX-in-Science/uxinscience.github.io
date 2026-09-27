export default function (eleventyConfig) {
  eleventyConfig.addCollection("newsPosts", (collectionApi) => {
    return collectionApi.getFilteredByTag("news").sort((a, b) =>
      b.data.published.localeCompare(a.data.published)
    );
  });

  eleventyConfig.addFilter("postDate", (value) => {
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      timeZone: "UTC"
    }).format(new Date(`${value}T00:00:00Z`));
  });

  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ CNAME: "CNAME" });

  return {
    dir: {
      input: "src",
      includes: "_includes",
      data: "_data",
      output: "_site"
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
}
