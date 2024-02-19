interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  keywords: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const data: ISiteMetadataResult = {
  siteTitle: 'Hiking Map',
  siteUrl: 'https://sport.sayidhe.com',
  logo: 'https://avatars.githubusercontent.com/u/8212913?v=4',
  description: 'Sayid & Nuo hikings',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Blog',
      url: 'https://sayidhe.com',
    },
    {
      name: 'Github',
      url: 'https://github.sayidhe.com/',
    },
  ],
};

export default data;
