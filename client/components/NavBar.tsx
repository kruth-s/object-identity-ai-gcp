"use client";

import { motion, useScroll, useTransform } from "motion/react";
import NavAvatar from "./NavAvatar";
import Link from "next/link";
import Image from "next/image";

const NavBar = () => {
  const { scrollY } = useScroll();

  const maxWidth = useTransform(
    scrollY,
    [0, 90],
    ["1536px", "1100px"]
  );

  return (
    <header className="fixed top-0 z-50 w-full">
      <motion.nav
        style={{ maxWidth }}
        className="mx-auto flex w-full max-w-screen-2xl items-center justify-between px-4 py-4 text-white bg-accent-foreground/80 backdrop-blur-3xl shadow-xl shadow-accent/20 2xl:rounded-lg 2xl:mt-3"
      >
        <Link href="/" className="flex items-center gap-2 text-accent">
          <Image
            src="/logo_2.svg"
            alt="Logo"
            width={28}
            height={28}
          />
          <h1 className="font-extrabold text-3xl">Findly</h1>
        </Link>

        {/* Nav links */}
        <div className="hidden lg:flex gap-8 text-sm lg:text-base font-medium">
          <button className="hover:text-accent transition">Report Item</button>
          <button className="hover:text-accent transition">View Listings</button>
          <button className="hover:text-accent transition">My Reports</button>
          <button className="hover:text-accent transition">Found an Item?</button>
          <button className="hover:text-accent transition">How It Works</button>
        </div>

        {/* Profile */}
        <NavAvatar />
      </motion.nav>
    </header>
  );
};

export default NavBar;