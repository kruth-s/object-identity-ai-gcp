"use client";

import CategorySelect from "@/components/CategorySelect";
import { FileUploadComponent } from "@/components/FileUpload";
import LocationInputGroup from "@/components/LocationInputGroup";
import NavBarExcludingHome from "@/components/NavBarExcludingHome";
import { Button } from "@/components/ui/button";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import { CalendarDays, Mail, PackagePlus, Megaphone } from "lucide-react";
import { useState } from "react";

const ReportItemPage = () => {
  const [category, setCategory] = useState("");
  const [status, setStatus] = useState("Lost");
  const [files, setFiles] = useState<File[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [location, setLocation] = useState<{
    street: string;
    city: string;
    state: string;
    pincode: string;
  }>({ street: "", city: "", state: "", pincode: "" });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (files.length === 0) {
      alert("Please upload at least one image of the item.");
      return;
    }

    if (!location.city || !location.state || !location.pincode) {
      alert("Please enter a valid location (PIN code is required).");
      return;
    }

    setIsSubmitting(true);

    try {
      const formData = new FormData();

      // Text fields
      formData.append("name", (e.currentTarget.itemName as HTMLInputElement).value);
      formData.append("category", category);
      formData.append("description", (e.currentTarget.description as HTMLTextAreaElement).value);
      formData.append("date_time", (e.currentTarget.datetime as HTMLInputElement).value);
      formData.append("status", status);

      // Location
      formData.append("street_area", location.street);
      formData.append("pin_code", location.pincode);
      formData.append("city", location.city);
      formData.append("state", location.state);

      // Contact
      formData.append("phone", (e.currentTarget.contact as HTMLInputElement).value);
      formData.append("email", (e.currentTarget.email as HTMLInputElement).value);

      // Files
      files.forEach((file) => formData.append("images", file));

      // Send request to FastAPI
      const apiUrl = process.env.NEXT_PUBLIC_API_URL!;
      const response = await fetch(`${apiUrl}/items/upload`, {
        method: "POST",
        body: formData, // multipart/form-data automatically
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to submit item: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const result = await response.json();
      alert(`SUCCESS! Item reported (ID: ${result.id})`);

      // Optional: Reset form
      setFiles([]);
      setCategory("");
      setStatus("Lost");
      setLocation({ street: "", city: "", state: "", pincode: "" });
      e.currentTarget.reset();

    } catch (error) {
      console.error("Submission failed:", error);
      alert(`Error: ${error instanceof Error ? error.message : "Unknown error"}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-screen">
      <NavBarExcludingHome />
      <div className="absolute inset-0 -z-10 h-full w-full bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]"></div>

      <div className="max-w-screen-2xl mx-auto">
        <div className="flex z-50 flex-col mx-12 border rounded-lg shadow-md p-8 mt-12 bg-secondary">
          <div className="flex items-center gap-2">
            <Megaphone />
            <h1 className="text-4xl font-bold">Report Item</h1>
          </div>
          <form className="flex justify-between mt-6" onSubmit={handleSubmit}>
            {/* Left side: Item Details */}
            <div className="flex-1 mr-10">
              <h2 className="text-2xl font-semibold mt-6">Enter Details of the Lost Item</h2>
              <div className="grid grid-cols-2 gap-4 mt-8">
                {/* Item Name */}
                <div>
                  <label htmlFor="itemName" className="xl:text-lg font-semibold mb-1 block">Item Name:</label>
                  <InputGroup>
                    <InputGroupAddon><PackagePlus /></InputGroupAddon>
                    <InputGroupInput
                      name="itemName"
                      id="itemName"
                      placeholder="Enter Item Name..."
                      required
                    />
                  </InputGroup>
                </div>
                {/* Category */}
                <CategorySelect
                  label="Category"
                  value={category}
                  options={["Electronics", "Documents", "Accessories", "Others"]}
                  onChange={setCategory}
                />
                {/* Description */}
                <div className="col-span-2">
                  <label htmlFor="description" className="xl:text-lg font-semibold mb-1 block">Description:</label>
                  <InputGroup>
                    <textarea
                      name="description"
                      id="description"
                      data-slot="input-group-control"
                      className="flex min-h-16 w-full resize-none rounded-md bg-transparent px-3 py-2.5 text-base transition-[color,box-shadow] outline-none md:text-sm font-semibold"
                      placeholder="Enter Description..."
                      required
                    />
                  </InputGroup>
                </div>
                {/* Date & Time */}
                <div>
                  <label htmlFor="datetime" className="xl:text-lg mb-1 block font-semibold">Date & Time:</label>
                  <InputGroup>
                    <InputGroupAddon><CalendarDays /></InputGroupAddon>
                    <InputGroupInput
                      type="datetime-local"
                      name="datetime"
                      id="datetime"
                      required
                    />
                  </InputGroup>
                </div>
                {/* Status */}
                <CategorySelect
                  label="Status"
                  value={status}
                  options={["Lost", "Found"]}
                  onChange={setStatus}
                />
                {/* Location */}
                <div className="col-span-2">
                  <LocationInputGroup onLocationChange={setLocation} />
                </div>
                {/* Contact */}
                <div>
                  <label htmlFor="contact" className="xl:text-lg mb-1 block font-semibold">Contact:</label>
                  <InputGroup>
                    <InputGroupAddon>
                      <label htmlFor="" className="font-bold">+91</label>
                    </InputGroupAddon>
                    <InputGroupInput
                      name="contact"
                      id="contact"
                      placeholder="Enter Phone Number..."
                      required
                    />
                  </InputGroup>
                </div>
                {/* Email */}
                <div>
                  <label htmlFor="email" className="xl:text-lg mb-1 block font-semibold">Email:</label>
                  <InputGroup>
                    <InputGroupAddon><Mail /></InputGroupAddon>
                    <InputGroupInput
                      type="email"
                      name="email"
                      id="email"
                      placeholder="Enter Email address..."
                      required
                    />
                  </InputGroup>
                </div>
                {/* Submit Button */}
                <div className="col-span-2">
                  <Button
                    type="submit"
                    className="mt-6 w-full bg-red-500 hover:bg-red-600 text-white font-bold text-lg py-6 cursor-pointer"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? "Processing..." : "Report Item"}
                  </Button>
                </div>
              </div>
            </div>
            {/* Right side: File Upload */}
            <div>
              <h2 className="text-2xl font-semibold mt-20">Upload Images of the Item</h2>
              <p className="text-base font-inter mt-2 mb-5">
                Upload clear images of the lost item to help others identify it easily.
              </p>
              <FileUploadComponent onFilesChange={setFiles} />
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ReportItemPage;
