"use client";

import * as React from "react";
import { MapPin, ChevronDown } from "lucide-react";

import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
  InputGroupButton,
} from "@/components/ui/input-group";

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";

/* -------------------- DATA -------------------- */

const INDIAN_STATES = [
  "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa",
  "Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala",
  "Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland",
  "Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
  "Uttar Pradesh","Uttarakhand","West Bengal","Delhi","Jammu & Kashmir",
  "Ladakh","Puducherry","Chandigarh",
  "Dadra & Nagar Haveli and Daman & Diu",
  "Lakshadweep","Andaman & Nicobar Islands",
];

const CITIES = [
  "Mumbai","Delhi","Bengaluru","Chennai","Hyderabad",
  "Pune","Kolkata","Ahmedabad",
];

/* -------------------- COMPONENT -------------------- */

export default function LocationInputGroup({
  onLocationChange,
}: {
  onLocationChange?: (loc: {
    street: string;
    city: string;
    state: string;
    pincode: string;
  }) => void;
}) {
  const [street, setStreet] = React.useState("");
  const [pincode, setPincode] = React.useState("");
  const [city, setCity] = React.useState("");
  const [state, setState] = React.useState("");
  const [loadingPin, setLoadingPin] = React.useState(false);

  /* -------------------- PIN → CITY/STATE -------------------- */
  const fetchFromPin = async (pin: string) => {
    if (pin.length !== 6) return;

    try {
      setLoadingPin(true);
      const res = await fetch(
        `https://api.postalpincode.in/pincode/${pin}`
      );
      const data = await res.json();

      if (data[0]?.Status === "Success") {
        const postOffice = data[0].PostOffice[0];
        setCity(postOffice.District);
        setState(postOffice.State);
      }
    } catch (err) {
      console.error("Invalid PIN");
    } finally {
      setLoadingPin(false);
    }
  };

  /* -------------------- OUTPUT (FOR BACKEND) -------------------- */
  React.useEffect(() => {
    const locationPayload = {
      street,
      city,
      state,
      pincode,
    };

    // send this object to parent / form / backend
    onLocationChange?.(locationPayload);
  }, [street, city, state, pincode, onLocationChange]);

  return (
    <div>
      <label className="xl:text-lg mb-1 block font-semibold">Location:</label>

      <div className="flex flex-col gap-2 xl:flex-row">
        {/* STREET */}
        <InputGroup className="flex-1">
          <InputGroupAddon>
            <MapPin />
          </InputGroupAddon>
          <InputGroupInput
            placeholder="Street / Area"
            value={street}
            onChange={(e) => setStreet(e.target.value)}
          />
        </InputGroup>

        {/* PIN CODE */}
        <InputGroup className="flex-1">
          <InputGroupInput
            placeholder="PIN Code"
            value={pincode}
            maxLength={6}
            onChange={(e) => {
              const val = e.target.value.replace(/\D/g, "");
              setPincode(val);
              fetchFromPin(val);
            }}
          />
          <InputGroupAddon align="inline-end">
            {loadingPin ? "..." : "IN"}
          </InputGroupAddon>
        </InputGroup>

        {/* CITY */}
        <DropdownMenu modal={false}>
          <DropdownMenuTrigger asChild>
            <div className="flex-1 cursor-pointer">
              <InputGroup>
                <InputGroupInput
                  readOnly
                  placeholder="City"
                  value={city}
                />
                <InputGroupAddon align="inline-end">
                  <InputGroupButton variant="ghost" size="icon-xs">
                    <ChevronDown />
                  </InputGroupButton>
                </InputGroupAddon>
              </InputGroup>
            </div>
          </DropdownMenuTrigger>

          <DropdownMenuContent className="w-56">
            {CITIES.map((c) => (
              <DropdownMenuItem key={c} onClick={() => setCity(c)}>
                {c}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>

        {/* STATE */}
        <DropdownMenu modal={false}>
          <DropdownMenuTrigger asChild>
            <div className="flex-1 cursor-pointer">
              <InputGroup>
                <InputGroupInput
                  readOnly
                  placeholder="State"
                  value={state}
                />
                <InputGroupAddon align="inline-end">
                  <InputGroupButton variant="ghost" size="icon-xs">
                    <ChevronDown />
                  </InputGroupButton>
                </InputGroupAddon>
              </InputGroup>
            </div>
          </DropdownMenuTrigger>

          <DropdownMenuContent className="max-h-72 overflow-y-auto w-64">
            {INDIAN_STATES.map((s) => (
              <DropdownMenuItem key={s} onClick={() => setState(s)}>
                {s}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
}
