import { AnyComponentList, ComponentProps } from "./components/any-component";
import { ButtonProps } from "@/components/tui/button";
import { AvatarProps } from "@/components/tui/avatar";
import { ContainerProps } from "@/components/tui/container";
import { LogoProps } from "./components/tui/logo";
import { useEffect, useState } from "react";

export function Tui() {
    return <Fetch />;
}

function Fetch1() {
    const buttonComp: ButtonProps = {
        _type: "button",
        variant: "default",
        children: "Test3",
    };
    const avatarComp: AvatarProps = {
        _type: "avatar",
        src: "https://www.gstatic.com/webp/gallery/1.jpg",
        alt: "Avatar",
        fallback: "T",
    };
    const logoComp: LogoProps = {
        _type: "logo",
        text: "tui",
        size: "lg",
    };
    const div1Comp: ContainerProps = {
        _type: "container",
        components: [logoComp],
        className: "p-6",
    };
    const div2Comp: ContainerProps = {
        _type: "container",
        components: [buttonComp, avatarComp],
        className: "flex",
        tag: "section",
    };
    return <Render propsList={[div1Comp, div2Comp]} />;
}

function Fetch() {
    const [propsList, setPropsList] = useState<ComponentProps[]>([]);

    useEffect(() => {
        async function fetchComponents() {
            const response = await fetch("http://localhost:8000/api/");
            const data = await response.json();
            console.log(data);
            setPropsList(data);
        }
        fetchComponents();
    }, []);
    return <Render propsList={propsList} />;
}

function Render(params: { propsList: ComponentProps[] }) {
    return <AnyComponentList propsList={params.propsList} />;
}
