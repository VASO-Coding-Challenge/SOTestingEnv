// questions.ts

export interface Document {
  /**
   * Represents a document with content and title
   */
  content: string;
  title: string;
}

export interface Question {
  /**
   * Represents a question with a unique number, a writeup, and associated documents
   */
  num: number;
  writeup: string;
  starter_code: string;
  docs: Document[]; // List of question-specific documents
}

export interface QuestionsPublic {
  /**
   * Response model containing a list of questions and global documentation
   */
  questions: Question[];
  global_docs: Document[]; // Documentation applicable to all questions
}
