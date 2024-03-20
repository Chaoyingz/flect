import { AvatarProps } from "@/components/flect/avatar";
import { ButtonProps } from "@/components/flect/button";
import { ContainerProps } from "@/components/flect/container";
import { HeadingProps } from "@/components/flect/heading";
import { LinkProps } from "@/components/flect/link";
import { TextProps } from "@/components/flect/text";
import { TableProps } from "@/components/flect/table";
import { OutletProps } from "@/components/flect/outlet";
import { FormProps } from "@/components/flect/form";
import { NavLinkProps } from "@/components/flect/nav-link";
import { ParagraphProps } from "@/components/flect/paragraph";
import { MarkdownProps } from "@/components/flect/markdown";
import { CopyButtonProps } from "@/components/flect/copy-button";
import { CodeBlockProps } from "@/components/flect/code-block";
import { CustomProps } from "@/components/flect/custom";
import { DialogProps } from "@/components/flect/dialog";

export type Json =
  | string
  | number
  | boolean
  | null
  | Json[]
  | {
      [k: string]: Json;
    };

export type AnyComponentProps =
  | AvatarProps
  | ButtonProps
  | CodeBlockProps
  | ContainerProps
  | CopyButtonProps
  | CustomProps
  | DialogProps
  | FormProps
  | HeadingProps
  | LinkProps
  | MarkdownProps
  | NavLinkProps
  | OutletProps
  | ParagraphProps
  | TableProps
  | TextProps;

export type AnyActionProps =
  | NotifyActionProps
  | RedirectActionProps
  | DispatchEventActionProps;

export type ActionResponse = {
  action: AnyActionProps;
};
