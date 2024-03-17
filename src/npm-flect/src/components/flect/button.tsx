import {
  Button as ButtonUI,
  ButtonProps as ButtonPropsUI,
} from "@/components/ui/button";
import { AnyComponents } from "@/components/flect/any-component";
import { AnyActionProps, AnyComponentProps } from "@/types";
import { useAction } from "@/hooks/use-action";

export interface ButtonProps extends Omit<ButtonPropsUI, "children"> {
  package: "flect";
  type: "button";
  onClickAction?: AnyActionProps;
  className?: string;
  children?: AnyComponentProps[];
}

export function Button({ children, onClickAction, ...rest }: ButtonProps) {
  const resolvedAction = useAction(onClickAction);
  return (
    <ButtonUI {...rest} onClick={() => resolvedAction()}>
      <AnyComponents children={children} />
    </ButtonUI>
  );
}
