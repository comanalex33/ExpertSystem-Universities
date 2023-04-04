export interface TokenModel {
    token: number;
  }
  
  export interface QuestionModel {
    question: boolean;
    text: string;
  }
  
  export interface ErrorModel {
    message: string;
  }
  
  export interface UniversityModel {
    name: string;
    country: string;
    program: string;
    faculty: string;
  }
  
  export interface ResultModel {
    programs: string[];
    universities: UniversityModel[];
  }
  
  export const server =
    "http://ec2-3-70-227-38.eu-central-1.compute.amazonaws.com/";
  