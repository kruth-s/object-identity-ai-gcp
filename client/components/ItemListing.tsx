import React from "react";
import {
  Card,
  CardAction,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import Image from "next/image";
import { Button } from "./ui/button";
import { MapPin, MoveRight } from "lucide-react";
import Link from "next/link";

const ItemListing = () => {
  return (
    <Link href={`/items-lost/${1}`}>
      <Card className="group max-w-3xl mx-auto mt-10 py-0! shadow-lg rounded-xl transition-shadow duration-300 cursor-pointer">
        <div className="overflow-hidden rounded-xl">
          <Image
            src={
              "https://images.unsplash.com/photo-1624505474107-840f25fbfb96?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            }
            alt="Image"
            width={500}
            height={500}
            className="size-72 w-full object-cover rounded-xl transition-transform duration-500 ease-out group-hover:scale-110 group-hover:brightness-90 "
          />
        </div>

        <div className="p-3 -mt-5">
          <p className="text-2xl font-extrabold">Keychain</p>
          <p className="my-3 font-light">
            Lorem ipsum dolor sit, amet consectetur adipisicing elit. Ipsum illo
            esse recusandae labore consequuntur voluptates sed. Magni sit iste
            nostrum?
          </p>
          <div className="mt-4">
            <MapPin className="inline mb-1 mr-1" size={20} />
            <p className="inline font-medium">Majestic, Bengaluru</p>
          </div>
          <Button className="mt-4 w-full text-white font-semibold py-4 cursor-pointer">
            View Details <MoveRight />
          </Button>
        </div>
      </Card>
    </Link>
  );
};

export default ItemListing;
