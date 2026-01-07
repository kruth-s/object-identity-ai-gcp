import Image from "next/image";
import { Button } from "./ui/button";
import { Highlighter } from "./ui/highlighter";
import { Megaphone, PackageSearch, PackageX } from "lucide-react";
import Link from "next/link";

const Hero = () => {
  return (
    <div className="flex justify-between items-center min-h-screen">
      <div className="absolute hero-bg min-h-screen brightness-95" />
      <div className="flex max-:xl:flex-col z-10 justify-between items-center w-screen mx-12">
        <div className="left flex flex-col gap-6 text-5xl md:text-6xl lg:text-7xl font-extrabold text-primary">
          <div className="heading">
            <h1 className="max-w-3xl">
              Helping{" "}
              <Highlighter action="highlight" color={"#FF9800"}>
                Lost Items
              </Highlighter>{" "}
              Find Their Way Home.
            </h1>
          </div>
          <div className="subheading">
            <p className="max-w-lg text-lg md:text-xl font-medium text-accent-foreground">
              Report lost items or help reunite found belongings with their
              owners — fast, secure, and community-driven.
            </p>
          </div>
          <div className="flex flex-col max-w-fit">
            <div>
              <Link href="/items-lost">
                <Button className="shadow-md py-6 bg-red-500 hover:bg-red-600 w-full text-accent text-lg m-0! cursor-pointer">
                  <span className="flex items-center gap-2 font-bold">
                    <PackageX /> Browse Lost Items
                  </span>
                </Button>
              </Link>
            </div>

            <div className="flex gap-4 -mt-5">
              <Link href="/report">
                <Button className="py-6 px-12 text-lg hover:bg-gray-700 cursor-pointer">
                  <span className="flex items-center gap-2 font-bold">
                    <Megaphone /> Report Lost Item
                  </span>
                </Button>
              </Link>

              <Link href="/items-found">
                <Button className="shadow-md py-6 px-12 bg-white text-accent-foreground hover:bg-gray-200 text-lg m-0! cursor-pointer">
                  <span className="flex items-center gap-2 font-bold ">
                    <PackageSearch /> Browse Found Items
                  </span>
                </Button>
              </Link>
            </div>
          </div>
        </div>
        <div className="right flex h-screen">
          <Image
            src={"/images/Hero.jpg"}
            alt="Hero Image"
            height={1200}
            width={800}
            className="bg-cover rounded-xl shadow-md my-auto"
            priority
          />
        </div>
      </div>
    </div>
  );
};

export default Hero;
