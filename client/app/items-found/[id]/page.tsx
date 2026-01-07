"use client";

import NavBarExcludingHome from "@/components/NavBarExcludingHome";
import { Mail, MessageSquareMore, Package, UserSearch } from "lucide-react";
import { useParams } from "next/navigation";

import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";

// Swiper styles (VERY IMPORTANT)
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import { Button } from "@/components/ui/button";

const Page = () => {
  const params = useParams<{ id: string }>();

  return (
    <div className="w-screen min-h-screen relative">
      {/* Navbar */}
      <NavBarExcludingHome />

      {/* Background pattern */}
      <div className="absolute inset-0 -z-10 bg-white bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:16px_16px]" />

      {/* Content */}
      <div className="relative z-10 flex flex-col max-w-screen-2xl mx-auto border rounded-lg shadow-md p-8 mt-12 bg-secondary">
        {/* Header */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1">
            <Package size={30} />
            <h1 className="text-3xl font-bold">Key Chain</h1>
          </div>
          <h3 className="font-semibold text-muted-foreground">
            Item ID: {params.id}
          </h3>
        </div>

        {/* Main Section */}
        <div className="flex gap-10 mt-6">
          {/* Swiper Section */}
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-semibold mb-4">Images</h2>

            <Swiper
              modules={[Navigation, Pagination]}
              spaceBetween={20}
              slidesPerView={3}
              navigation
              pagination={{ clickable: true }}
              className="w-full custom-swiper"
            >
              {[1, 2, 3, 4, 5].map((i) => (
                <SwiperSlide key={i}>
                  <div className="h-60 bg-white rounded-xl shadow flex items-center justify-center text-xl font-semibold">
                    Image {i}
                  </div>
                </SwiperSlide>
              ))}
            </Swiper>

            <h2 className="text-2xl font-semibold my-4">Other Details:</h2>
            <div className="text-base font-inter space-y-2 text-muted-foreground">
              <p>
                Description: A black key chain with a small flashlight attached.
              </p>
              <p>Location Found: Majestic, Bengaluru</p>
              <p>Date Found: 15th June 2024</p>
              <p>Category: Accessories</p>

              <p className="text-xl font-bold text-black text-center">
                Render other JSON Data Here...
              </p>
            </div>
          </div>

          {/* Founder Details */}
          <div className="w-[350px] bg-white p-6 rounded-xl shadow">
            <h2 className="inline-flex items-center gap-2 text-2xl font-semibold">
              <UserSearch />
              Founder Details
            </h2>
            <p className="text-base font-inter mt-2 mb-5 text-muted-foreground">
              These are the details of the person who found the item.
            </p>
            <p>Name: Lorem Ipsum</p>
            <p>Location: Bengaluru</p>
            <p>Contact No: 123456789</p>
            <p>Email: user@example.com</p>

            <Button className="mt-4 font-semibold hover:bg-neutral-700 cursor-pointer w-full">
              <MessageSquareMore /> Chat with Founder
            </Button>
            <Button className="mt-4 font-semibold bg-neutral-200 text-black hover:bg-neutral-400 cursor-pointer w-full">
              <Mail /> Draft an Email
            </Button>

            {/* Future upload / details */}
            {/* <FileUploadComponent /> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Page;
