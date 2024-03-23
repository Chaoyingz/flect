import { Resolver, appendErrors, FieldError } from "react-hook-form";
import Ajv, { DefinedError } from "ajv";
import ajvErrors from "ajv-errors";

const parseErrorSchema = (
  ajvErrors: DefinedError[],
  validateAllFieldCriteria: boolean,
): Record<string, FieldError> => {
  // Ajv will return empty instancePath when require error
  ajvErrors.forEach((error) => {
    if (error.keyword === "required") {
      error.instancePath += "/" + error.params.missingProperty;
    }
  });

  return ajvErrors.reduce<Record<string, FieldError>>((previous, error) => {
    // `/deepObject/data` -> `deepObject.data`
    const path = error.instancePath.substring(1).replace(/\//g, ".");

    if (!previous[path]) {
      previous[path] = {
        message: error.message,
        type: error.keyword,
      };
    }

    if (validateAllFieldCriteria) {
      const types = previous[path].types;
      const messages = types && types[error.keyword];

      previous[path] = appendErrors(
        path,
        validateAllFieldCriteria,
        previous,
        error.keyword,
        messages
          ? ([] as string[]).concat(messages as string[], error.message || "")
          : error.message,
      ) as FieldError;
    }

    return previous;
  }, {});
};

export function ajvResolver(schema: object, addVocabulary: string[]): Resolver {
  const ajv = new Ajv({ allErrors: true });
  ajv.addVocabulary(addVocabulary);
  ajvErrors(ajv);
  return async (values, _, options) => {
    const validate = ajv.compile(schema);
    const valid = validate(values);

    if (valid) {
      return { values, errors: {} };
    } else {
      const errors = parseErrorSchema(
        validate.errors as DefinedError[],
        options.criteriaMode === "all",
      );
      return {
        values: {},
        errors,
      };
    }
  };
}
