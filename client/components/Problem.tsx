import { cn } from "@/lib/utils";
import React from "react";
import { Highlighter } from "@/components/ui/highlighter";
import { Search, MapPin, Clock } from "lucide-react";

const items = [
  {
    icon: Search,
    title: "Items Go Missing",
    description:
      "People frequently lose personal belongings in public places, offices, or transit hubs, with no centralized way to report or search for them.",
  },
  {
    icon: MapPin,
    title: "No Clear Location Tracking",
    description:
      "Lost items are often found by others, but without accurate location or category information, reuniting them with owners becomes difficult.",
  },
  {
    icon: Clock,
    title: "Delayed Recoveries",
    description:
      "Without a streamlined system, lost and found items remain unclaimed for long periods, reducing the chances of timely recovery.",
  },
];

const Problem = () => {
  return (
    <div className="">
      <h2
        className={cn(
          "text-center my-6",
          "font-semibold text-[#EA1A24]",
          "uppercase underline underline-offset-2"
        )}
      >
        Problem
      </h2>

      <h2
        className={cn(
          "text-3xl md:text-5xl xl:text-6xl text-center",
          "font-bold",
          "text-balance"
        )}
      >
        Finding lost items shouldn't be{" "}
        <Highlighter action="highlight" color="#FF9800">
          complicated
        </Highlighter>
        .
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12 xl:gap-32 mt-20 xl:mt-32 mx-auto max-w-7xl px-24 xl:px-12">
        {items.map((item, index) => {
          const Icon = item.icon;
          return (
            <div key={index} className="flex flex-col gap-4">
              <div className="grid place-items-center p-3 bg-red-200 w-fit rounded-xl dark:bg-red-600 text-[#EA1A24] dark:text-white">
                <Icon />
              </div>
              <h3 className="font-semibold text-xl xl:text-2xl">
                {item.title}
              </h3>
              <p className="text-base xl:text-lg font-inter">
                {item.description}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Problem;
