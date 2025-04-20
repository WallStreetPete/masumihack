export type Campaign = {
  title: string;
  prospects: Prospect[];
};

export type Email = {
  text: string;
  from: string;
};

export type Prospect = {
  firstName: string;
  lastName: string;
  organizationName: string;
  linkedinUrl: string;
  email: string | null;
  phone: string | null;
  title: string | null;
  seniority: string | null;
  personalEmails: string[];
  city: string | null;
  state: string | null;
  country: string | null;
  companySize: string | null;
  companyIndustry: string | null;
  companyWebsite: string | null;
  emailMessages: Email[];
};
