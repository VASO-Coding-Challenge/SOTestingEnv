import type React from "react";

import { useState } from "react";
import { ChevronUp, ChevronDown } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface CounterInputProps {
  initialValue?: number;
  min?: number;
  max?: number;
  step?: number;
  onChange?: (value: number) => void;
}

export default function CounterInput({
  initialValue = 0,
  min = 0,
  max = 100,
  step = 1,
  onChange,
}: CounterInputProps) {
  const [value, setValue] = useState(initialValue);

  const increment = () => {
    const newValue = Math.min(value + step, max);
    setValue(newValue);
    onChange?.(newValue);
  };

  const decrement = () => {
    const newValue = Math.max(value - step, min);
    setValue(newValue);
    onChange?.(newValue);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;

    // Allow empty input or valid numbers
    if (inputValue === "" || /^\d+$/.test(inputValue)) {
      const numValue =
        inputValue === ""
          ? min
          : Math.max(Math.min(Number.parseInt(inputValue, 10), max), min);
      setValue(numValue);
      onChange?.(numValue);
    }
  };

  return (
    <div className="relative flex w-full max-w-[200px]">
      <Input
        type="text"
        value={value}
        onChange={handleChange}
        className="pr-12 text-lg"
        aria-label="Counter value"
      />
      <div className="absolute right-0 top-0 flex h-full flex-col border-l">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="h-1/2 rounded-none rounded-tr-md border-b px-2"
          onClick={increment}
          aria-label="Increment"
        >
          <ChevronUp className="h-4 w-4" />
        </Button>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="h-1/2 rounded-none rounded-br-md px-2"
          onClick={decrement}
          aria-label="Decrement"
        >
          <ChevronDown className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
