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


export const mockMessages = [
    {
      user: "Bento",
      message: "Welcome to the OPT Application Guide!\n- Make sure to have your I-20 form ready.\n- Don't forget to check the filing dates.",
    },
    {
      user: "You",
      message: "Got it! What are the required documents for the application?",
    },
    {
      user: "Bento",
      message: "You will need:\n- Your I-20 form\n- A completed Form I-765\n- Two passport-sized photos\n- Your passport\n- Any previous EAD cards",
    },
    {
      user: "You",
      message: "Thanks! How long does it usually take to process the application?",
    },
    {
      user: "Bento",
      message: "Processing time can vary, but generally it takes about 3-5 months.\n- Make sure to track your application status online.",
    },
  ];