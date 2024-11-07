// Submission.tsx

import { Question, Document } from "./questions";

export interface Submission {
  /**
   * Represents a single code submission tied to a specific question
   */
  question: Question;
  code?: string;
  languageId?: number;
  file?: File | null;
  output?: string;
}

export interface SubmissionWidgetProps {
  /**
   * Props needed by the SubmissionWidget component
   */
  question: Question;
  globalDocs: Document[];
}
