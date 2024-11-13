// prismjs is a 3rd party library for getting markdowns to work.
declare module "prismjs" {
  export function highlightAll(
    async?: boolean,
    callback?: (element: Element) => void
  ): void;
}
