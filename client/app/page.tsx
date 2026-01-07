import Footer from "@/components/Footer"
import Hero from "@/components/Hero"
import Marquee from "@/components/Marquee"
import NavBar from "@/components/NavBar"
import Problem from "@/components/Problem"
import ScrollPin from "@/components/ScrollPin"
import Solution from "@/components/Solution"
import * as motion from "motion/react-client"

const Home = () => {
  return (
    <div className='bg-secondary h-screen'>
      <div className='flex flex-col'>
        <NavBar />
         {/* <motion.div
            style={box}
            animate={{ rotate: 360 }}
            transition={{ repeat: Infinity, duration: 1 }}
        /> */}
        <div className="">
          <Hero />
        </div>
        <Marquee />
        <Problem />
        <Solution />
        <ScrollPin />
        <Footer />
      </div>
    </div>
  )
}

export default Home

const box = {
    width: 100,
    height: 100,
    backgroundColor: "#ff0088",
    borderRadius: 5,
}