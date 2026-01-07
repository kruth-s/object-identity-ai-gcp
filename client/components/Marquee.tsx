import {
  ScrollVelocityContainer,
  ScrollVelocityRow,
} from "@/components/ui/scroll-based-velocity";
import { cn } from "@/lib/utils";
import { Circle } from "lucide-react";

const items = [
  "Report",
  "Recover",
  "Reconnect",
  "Belongings",
  "Community",
  "Trust",
  "Found",
  "Lost",
  "Verified",
  "Reunited",
  "Secure",
  "Hope",
];

const Marquee = () => {
  return (
    <div className="relative dark:bg-black overflow-hidden md:mt-5 mb-24">
      <h2
        className={cn(
          "text-center my-6",
          "font-semibold text-[#EA1A24]",
          "uppercase"
        )}
      >
        Together, We Bring Lost Items Home
      </h2>

      <ScrollVelocityContainer className="text-3xl md:text-4xl xl:text-6xl font-bold relative z-10">
        <ScrollVelocityRow baseVelocity={5} direction={1} className="py-2">
          {items.map((item, index) => (
            <span key={index} className="flex items-center">
              {item}{" "}
              <span className="mx-4 mt-3">
                <Circle fill="#FE330A" stroke="0" />
              </span>
            </span>
          ))}
        </ScrollVelocityRow>
        <ScrollVelocityRow baseVelocity={5} direction={-1} className="py-2">
          {items.map((item, index) => (
            <span key={index} className="flex items-center">
              {item}{" "}
              <span className="mx-4 mt-3">
                <Circle fill="#FE330A" stroke="0" />
              </span>
            </span>
          ))}
        </ScrollVelocityRow>
      </ScrollVelocityContainer>

      {/* Left shadow */}
      <div className="absolute top-0 left-0 h-full w-54 bg-linear-to-r from-neutral-100 to-transparent dark:from-black pointer-events-none z-20"></div>

      {/* Right shadow */}
      <div className="absolute top-0 right-0 h-full w-54 bg-linear-to-l from-neutral-100 to-transparent dark:from-black pointer-events-none z-20"></div>
    </div>
  );
};

export default Marquee;