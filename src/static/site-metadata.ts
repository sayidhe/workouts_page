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
  siteTitle: 'Workouts Map',
  siteUrl: 'https://sport.sayidhe.com',
  logo: 'https://avatars.githubusercontent.com/u/8212913?v=4',
  description: 'Personal workouts',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Blog',
      url: 'https://sayidhe.com',
    },
    {
      name: 'About',
      url: 'https://github.com/sayidhe/workouts_page/blob/master/README-CN.md',
    },
  ],
};

export default data;
