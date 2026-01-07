import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const NavAvatar = () => {
  return (
    <div>
      <DropdownMenu modal={false}>
        <DropdownMenuTrigger asChild>
          <Avatar className="hover:cursor-pointer select-none">
            <AvatarImage src="https://github.com/shadcn.png" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="end">
          <DropdownMenuGroup className="max-md:block hidden">
            <DropdownMenuLabel className="font-bold">Nav Links</DropdownMenuLabel>
            <DropdownMenuItem>
              Report Item
              <DropdownMenuShortcut>⇧⌘R</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem>
              View Listings
              <DropdownMenuShortcut>⇧⌘V</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem>
              My Reports
              <DropdownMenuShortcut>⇧⌘M</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem>
              Found an Item?
              <DropdownMenuShortcut>⇧⌘F</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem>
              How It Works
              <DropdownMenuShortcut>⇧⌘H</DropdownMenuShortcut>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator className="max-md:block hidden"/>
          <DropdownMenuGroup>
          <DropdownMenuLabel className="font-bold">My Account</DropdownMenuLabel>
            <DropdownMenuItem>
              Profile
              <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem>
              Settings
              <DropdownMenuShortcut>⌘S</DropdownMenuShortcut>
            </DropdownMenuItem>
            <DropdownMenuItem>
              Keyboard shortcuts
              <DropdownMenuShortcut>⌘K</DropdownMenuShortcut>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem>GitHub</DropdownMenuItem>
          <DropdownMenuItem>Support</DropdownMenuItem>
          <DropdownMenuItem disabled>API</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem className="text-red-500 font-bold">
            Log out
            <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default NavAvatar;
