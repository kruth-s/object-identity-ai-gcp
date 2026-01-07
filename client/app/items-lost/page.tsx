import Footer from "@/components/Footer";
import FooterEXcludingHome from "@/components/FooterExcludingHome";
import ItemListing from "@/components/ItemListing";
import NavBarExcludingHome from "@/components/NavBarExcludingHome";
import { Button } from "@/components/ui/button";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import { Search } from "lucide-react";

const page = () => {
  return (
    <div>
      <NavBarExcludingHome />
      <div className="mx-10 p-6">
        <h1 className="text-4xl font-bold mt-3">Lost Items</h1>
        <div className="flex items-center gap-4 max-w-5xl mx-auto mt-10">
          <div className="flex-1 shadow-xl">
            <InputGroup className="py-6">
              <InputGroupAddon>
                <Search />
              </InputGroupAddon>
              <InputGroupInput
                className="text-xl!"
                placeholder="Search for items..."
              />
            </InputGroup>
          </div>
          <div className="">
            <Button className="py-6">
              <Search />
              <p className="text-xl font-bold">Search</p>
            </Button>
          </div>
        </div>
        <div className="grid grid-cols-5 gap-10">
          <ItemListing />
          <ItemListing />
          <ItemListing />
          <ItemListing />
          <ItemListing />
          <ItemListing />
          <ItemListing />
          <ItemListing />
        </div>
      </div>
      <FooterEXcludingHome />
    </div>
  );
};

export default page;
