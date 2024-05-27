export const mockFolders = [
    { emoji: "🏝️", name: "Puerto Rico", link: "/puerto_rico" },
    { emoji: "🛃", name: "OPT Application", link: "/opt_application" },
    { emoji: "💻", name: "Algorithms", link: "/algorithms" },
]

export const mockFolder = {
  emoji: "🛃",
  name: "OPT Application",
  description:
    "Contains personal paperwork, online articles, and recommended timelines to apply for OPT for upcoming summer internship",
  items: [
    {
      type: "link" as const,
      content: {
        name: "USCIS OPT Overview",
        favicon: "https://intertradecustoms.com/img/cbplogo.png",
        summary: "Official USCIS page on OPT.",
      },
    },
    {
      type: "screenshot" as const,
      content: {
        name: "OPT Application Form",
        summary: "Screenshot of the filled OPT application form.",
        previewImg: "https://example.com/screenshot.png",
      },
    },
    {
      type: "file" as const,
      content: {
        name: "OPT Timeline PDF",
        summary: "PDF document outlining the recommended timeline for OPT application.",
      },
    },
  ],
};
