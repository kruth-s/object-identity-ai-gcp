"use client";

import * as React from "react";
import { Boxes, MoreHorizontal } from "lucide-react";

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";

import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
  InputGroupButton,
} from "@/components/ui/input-group";

type CategorySelectProps = {
  label?: string;
  placeholder?: string;
  options: string[];
  value?: string;
  onChange?: (value: string) => void;
};

export default function CategorySelect({
  label = "Category",
  placeholder = "Select Category...",
  options,
  value,
  onChange,
}: CategorySelectProps) {
  const [selected, setSelected] = React.useState(value ?? "");

  const handleSelect = (option: string) => {
    setSelected(option);
    onChange?.(option);
  };

  return (
    <div>
      {label && (
        <label className="xl:text-lg mb-1 block font-semibold">
          {label}:
        </label>
      )}

      <DropdownMenu modal={false}>
        <DropdownMenuTrigger asChild>
          <div>
            <InputGroup className="cursor-pointer">
              <InputGroupAddon>
                <Boxes />
              </InputGroupAddon>

              <InputGroupInput
                readOnly
                value={selected}
                placeholder={placeholder}
              />

              <InputGroupAddon align="inline-end">
                <InputGroupButton
                  variant="ghost"
                  aria-label="Open"
                  size="icon-xs"
                >
                  <MoreHorizontal />
                </InputGroupButton>
              </InputGroupAddon>
            </InputGroup>
          </div>
        </DropdownMenuTrigger>

        <DropdownMenuContent
          align="start"
          className="w-full min-w-xs xl:min-w-md"
        >
          {options.map((option) => (
            <DropdownMenuItem
              key={option}
              onClick={() => handleSelect(option)}
            >
              {option}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
