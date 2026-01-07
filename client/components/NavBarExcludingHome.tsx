import Image from "next/image";
import Link from "next/link";
import React from "react";
import NavAvatar from "./NavAvatar";

const NavBarExcludingHome = () => {
  return (
    <div className="px-6 py-3 flex justify-between items-center bg-secondary shadow-md backdrop-blur-3xl">
      <Link href="/" className="flex items-center gap-2 text-accent">
        <Image src="/logo_3.png" alt="Logo" width={150} height={150} />
      </Link>
      <NavAvatar />
    </div>
  );
};

export default NavBarExcludingHome;
